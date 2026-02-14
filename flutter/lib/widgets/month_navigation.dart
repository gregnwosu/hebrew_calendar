import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../providers/calendar_providers.dart';

class MonthNavigation extends ConsumerWidget {
  const MonthNavigation({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final month = ref.watch(currentMonthProvider);
    final label = DateFormat('MMMM yyyy').format(month);

    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
          icon: const Icon(Icons.chevron_left),
          onPressed: () => _changeMonth(ref, -1),
        ),
        const SizedBox(width: 8),
        Text(
          label,
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(width: 8),
        IconButton(
          icon: const Icon(Icons.chevron_right),
          onPressed: () => _changeMonth(ref, 1),
        ),
      ],
    );
  }

  void _changeMonth(WidgetRef ref, int delta) {
    final current = ref.read(currentMonthProvider);
    var year = current.year;
    var month = current.month + delta;
    if (month < 1) {
      month = 12;
      year--;
    } else if (month > 12) {
      month = 1;
      year++;
    }
    ref.read(currentMonthProvider.notifier).state = DateTime(year, month);
    ref.read(selectedDateProvider.notifier).state = DateTime(year, month, 1);
  }
}
