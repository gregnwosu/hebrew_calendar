import 'package:flutter_test/flutter_test.dart';

import 'package:hebrewcalendar/models/moon_phase.dart';
import 'package:hebrewcalendar/models/feast_day.dart';
import 'package:hebrewcalendar/models/calendar_day.dart';
import 'package:hebrewcalendar/data/calendar_repository.dart';
import 'package:hebrewcalendar/data/calendar_data_loader.dart';

void main() {
  group('MoonPhase', () {
    test('fromString returns correct phase', () {
      expect(MoonPhase.fromString('New Moon'), MoonPhase.newMoon);
      expect(MoonPhase.fromString('Full Moon'), MoonPhase.fullMoon);
      expect(MoonPhase.fromString('Waxing Crescent'), MoonPhase.waxingCrescent);
    });

    test('each phase has emoji and display name', () {
      for (final phase in MoonPhase.values) {
        expect(phase.emoji.isNotEmpty, true);
        expect(phase.displayName.isNotEmpty, true);
      }
    });
  });

  group('FeastDay', () {
    test('fromJson parses correctly', () {
      final json = {
        'name': 'Passover (Pesach)',
        'description': 'Test description',
        'bibleRefs': ['Leviticus 23:5', 'Exodus 12:1-14'],
      };
      final feast = FeastDay.fromJson(json);
      expect(feast.name, 'Passover (Pesach)');
      expect(feast.description, 'Test description');
      expect(feast.bibleRefs.length, 2);
    });

    test('fromJson handles missing optional fields', () {
      final json = {'name': 'Test Feast'};
      final feast = FeastDay.fromJson(json);
      expect(feast.name, 'Test Feast');
      expect(feast.description, isNull);
      expect(feast.bibleRefs, isEmpty);
    });
  });

  group('CalendarDay', () {
    test('properties are accessible', () {
      final day = CalendarDay(
        date: DateTime(2025, 3, 13),
        phase: MoonPhase.newMoon,
        angle: 5.2,
        isSabbath: true,
        isNewMoon: true,
        feast: const FeastDay(name: 'Passover (Pesach)'),
      );
      expect(day.isSabbath, true);
      expect(day.isNewMoon, true);
      expect(day.feast?.name, 'Passover (Pesach)');
    });
  });

  group('CalendarRepository', () {
    late CalendarRepository repo;

    setUp(() {
      final days = <DateTime, CalendarDay>{};
      // Add a few test days
      days[DateTime(2025, 3, 13)] = CalendarDay(
        date: DateTime(2025, 3, 13),
        phase: MoonPhase.newMoon,
        angle: 5.2,
        isNewMoon: true,
        isSabbath: true,
      );
      days[DateTime(2025, 3, 14)] = CalendarDay(
        date: DateTime(2025, 3, 14),
        phase: MoonPhase.waxingCrescent,
        angle: 18.5,
      );

      final data = CalendarData(
        days: days,
        scriptures: {'Leviticus 23:5': 'In the fourteenth day...'},
      );
      repo = CalendarRepository(data);
    });

    test('getDay returns correct day', () {
      final day = repo.getDay(DateTime(2025, 3, 13));
      expect(day, isNotNull);
      expect(day!.isNewMoon, true);
    });

    test('getDay returns null for unknown date', () {
      final day = repo.getDay(DateTime(2020, 1, 1));
      expect(day, isNull);
    });

    test('getMonth returns list of days', () {
      final days = repo.getMonth(2025, 3);
      expect(days.length, 31); // March has 31 days
      expect(days[12], isNotNull); // March 13 (index 12)
      expect(days[12]!.isNewMoon, true);
    });

    test('getScripture returns text', () {
      expect(repo.getScripture('Leviticus 23:5'), isNotNull);
      expect(repo.getScripture('Unknown'), isNull);
    });
  });
}
