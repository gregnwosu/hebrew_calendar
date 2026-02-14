import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/calendar_data_loader.dart';
import '../data/calendar_repository.dart';
import '../models/calendar_day.dart';

/// Loaded once at startup.
final calendarDataProvider = FutureProvider<CalendarData>((ref) {
  return CalendarDataLoader.load();
});

final calendarRepositoryProvider = Provider<CalendarRepository?>((ref) {
  final dataAsync = ref.watch(calendarDataProvider);
  return dataAsync.whenOrNull(data: (data) => CalendarRepository(data));
});

/// The currently viewed month.
final currentMonthProvider =
    StateProvider<DateTime>((ref) => DateTime(DateTime.now().year, DateTime.now().month));

/// The currently selected day.
final selectedDateProvider = StateProvider<DateTime>((ref) => DateTime.now());

/// Days for the currently viewed month.
final monthDaysProvider = Provider<List<CalendarDay?>>((ref) {
  final repo = ref.watch(calendarRepositoryProvider);
  final month = ref.watch(currentMonthProvider);
  if (repo == null) return [];
  return repo.getMonth(month.year, month.month);
});

/// Detail for the selected day.
final selectedDayProvider = Provider<CalendarDay?>((ref) {
  final repo = ref.watch(calendarRepositoryProvider);
  final date = ref.watch(selectedDateProvider);
  if (repo == null) return null;
  return repo.getDay(date);
});
