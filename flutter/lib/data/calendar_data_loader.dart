import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart' show rootBundle;

import '../models/calendar_day.dart';
import '../models/feast_day.dart';
import '../models/moon_phase.dart';

class CalendarDataLoader {
  static Future<CalendarData> load() async {
    final jsonStr = await rootBundle.loadString('assets/calendar_data.json');
    final json = jsonDecode(jsonStr) as Map<String, dynamic>;

    // Verify MD5 integrity
    final storedMd5 = json['md5'] as String?;
    if (storedMd5 != null) {
      // Recompute MD5 over the data without the md5 field (same as export script)
      final dataWithoutMd5 = Map<String, dynamic>.from(json)..remove('md5');
      final dataJsonBytes =
          utf8.encode(jsonEncode(_sortedJson(dataWithoutMd5)));
      final computed = _md5(Uint8List.fromList(dataJsonBytes));
      if (computed != storedMd5) {
        throw StateError(
          'Calendar data integrity check failed.\n'
          'Expected: $storedMd5\n'
          'Got:      $computed',
        );
      }
      debugPrint('Calendar data MD5 verified: $storedMd5');
    }

    return CalendarData.fromJson(json);
  }

  /// Pure-Dart MD5 (RFC 1321). No external package needed.
  static String _md5(Uint8List data) {
    // Pre-processing: pad message
    final bitLen = data.length * 8;
    final padded = <int>[...data, 0x80];
    while (padded.length % 64 != 56) {
      padded.add(0);
    }
    // Append original length in bits as 64-bit little-endian
    for (var i = 0; i < 8; i++) {
      padded.add((bitLen >> (i * 8)) & 0xff);
    }

    final bytes = Uint8List.fromList(padded);
    final words = Uint32List.view(bytes.buffer);

    int a0 = 0x67452301;
    int b0 = 0xefcdab89;
    int c0 = 0x98badcfe;
    int d0 = 0x10325476;

    const s = [
      7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, //
      5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
      4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
      6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
    ];

    const k = [
      0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, //
      0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
      0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
      0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
      0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
      0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
      0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
      0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
      0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
      0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
      0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
      0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
      0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
      0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
      0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
      0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
    ];

    int add32(int a, int b) => (a + b) & 0xFFFFFFFF;
    int rotl32(int x, int n) =>
        ((x << n) & 0xFFFFFFFF) | ((x & 0xFFFFFFFF) >> (32 - n));

    for (var chunk = 0; chunk < words.length; chunk += 16) {
      var a = a0, b = b0, c = c0, d = d0;
      for (var i = 0; i < 64; i++) {
        int f, g;
        if (i < 16) {
          f = (b & c) | ((~b & 0xFFFFFFFF) & d);
          g = i;
        } else if (i < 32) {
          f = (d & b) | ((~d & 0xFFFFFFFF) & c);
          g = (5 * i + 1) % 16;
        } else if (i < 48) {
          f = b ^ c ^ d;
          g = (3 * i + 5) % 16;
        } else {
          f = c ^ (b | (~d & 0xFFFFFFFF));
          g = (7 * i) % 16;
        }
        final temp = d;
        d = c;
        c = b;
        b = add32(
            b, rotl32(add32(add32(a, f), add32(k[i], words[chunk + g])), s[i]));
        a = temp;
      }
      a0 = add32(a0, a);
      b0 = add32(b0, b);
      c0 = add32(c0, c);
      d0 = add32(d0, d);
    }

    String toHex(int v) {
      final bytes = [v & 0xff, (v >> 8) & 0xff, (v >> 16) & 0xff, (v >> 24) & 0xff];
      return bytes.map((b) => b.toRadixString(16).padLeft(2, '0')).join();
    }

    return '${toHex(a0)}${toHex(b0)}${toHex(c0)}${toHex(d0)}';
  }

  /// Recursively sort JSON keys to match Python's json.dumps(sort_keys=True).
  static dynamic _sortedJson(dynamic obj) {
    if (obj is Map<String, dynamic>) {
      final sorted = Map<String, dynamic>.fromEntries(
        obj.entries.toList()..sort((a, b) => a.key.compareTo(b.key)),
      );
      return sorted.map((k, v) => MapEntry(k, _sortedJson(v)));
    }
    if (obj is List) {
      return obj.map(_sortedJson).toList();
    }
    return obj;
  }
}

class CalendarData {
  CalendarData({
    required this.days,
    required this.scriptures,
  });

  final Map<DateTime, CalendarDay> days;
  final Map<String, String> scriptures;

  factory CalendarData.fromJson(Map<String, dynamic> json) {
    final daysJson = json['days'] as Map<String, dynamic>;
    final scripturesJson = json['scriptures'] as Map<String, dynamic>;

    final days = <DateTime, CalendarDay>{};
    for (final entry in daysJson.entries) {
      final date = DateTime.parse(entry.key);
      final d = entry.value as Map<String, dynamic>;

      FeastDay? feast;
      if (d.containsKey('feast')) {
        feast = FeastDay.fromJson(d['feast'] as Map<String, dynamic>);
      }

      days[date] = CalendarDay(
        date: date,
        phase: MoonPhase.fromString(d['phase'] as String),
        angle: (d['angle'] as num).toDouble(),
        feast: feast,
        isSabbath: d['isSabbath'] == true,
        isNewMoon: d['isNewMoon'] == true,
        isNewYear: d['isNewYear'] == true,
        newMoonAngle: d['newMoonAngle'] != null
            ? (d['newMoonAngle'] as num).toDouble()
            : null,
      );
    }

    final scriptures = scripturesJson.map(
      (k, v) => MapEntry(k, v as String),
    );

    return CalendarData(days: days, scriptures: scriptures);
  }
}
