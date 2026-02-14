import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/calendar_day.dart';
import '../models/feast_day.dart';
import '../models/moon_phase.dart';

class CalendarDataLoader {
  static Future<CalendarData> load() async {
    final jsonStr = await rootBundle.loadString('assets/calendar_data.json');
    final json = jsonDecode(jsonStr) as Map<String, dynamic>;
    return CalendarData.fromJson(json);
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
