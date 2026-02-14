import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/calendar_day.dart';
import '../providers/calendar_providers.dart';
import 'day_cell.dart';

class CalendarGrid extends ConsumerWidget {
  const CalendarGrid({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final month = ref.watch(currentMonthProvider);
    final days = ref.watch(monthDaysProvider);
    final selected = ref.watch(selectedDateProvider);

    // First day of the month: Monday = 1, Sunday = 7
    final firstWeekday = DateTime(month.year, month.month, 1).weekday;
    // Offset so Monday = 0
    final offset = firstWeekday - 1;

    const weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];

    return Column(
      children: [
        // Weekday header
        Row(
          children: weekdays
              .map((d) => Expanded(
                    child: Center(
                      child: Text(
                        d,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                      ),
                    ),
                  ))
              .toList(),
        ),
        const SizedBox(height: 4),
        // Calendar rows
        ..._buildWeeks(days, offset, selected, ref),
      ],
    );
  }

  List<Widget> _buildWeeks(
    List<CalendarDay?> days,
    int offset,
    DateTime selected,
    WidgetRef ref,
  ) {
    final totalSlots = offset + days.length;
    final weekCount = (totalSlots / 7).ceil();

    return List.generate(weekCount, (week) {
      return Row(
        children: List.generate(7, (col) {
          final index = week * 7 + col - offset;
          if (index < 0 || index >= days.length) {
            return const Expanded(child: SizedBox(height: 58));
          }
          final day = days[index];
          if (day == null) {
            return const Expanded(child: SizedBox(height: 58));
          }

          final isSelected = day.date.year == selected.year &&
              day.date.month == selected.month &&
              day.date.day == selected.day;

          return Expanded(
            child: SizedBox(
              height: 58,
              child: DayCell(
                day: day,
                isSelected: isSelected,
                onTap: () {
                  ref.read(selectedDateProvider.notifier).state = day.date;
                },
              ),
            ),
          );
        }),
      );
    });
  }
}
