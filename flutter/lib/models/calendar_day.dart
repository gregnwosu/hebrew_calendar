import 'feast_day.dart';
import 'moon_phase.dart';

class CalendarDay {
  const CalendarDay({
    required this.date,
    required this.phase,
    required this.angle,
    this.feast,
    this.isSabbath = false,
    this.isNewMoon = false,
    this.isNewYear = false,
    this.newMoonAngle,
  });

  final DateTime date;
  final MoonPhase phase;
  final double angle;
  final FeastDay? feast;
  final bool isSabbath;
  final bool isNewMoon;
  final bool isNewYear;
  final double? newMoonAngle;
}
