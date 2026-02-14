import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../models/calendar_day.dart';
import '../providers/calendar_providers.dart';
import '../theme/app_theme.dart';
import 'scripture_accordion.dart';

class DayDetailPanel extends ConsumerWidget {
  const DayDetailPanel({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final day = ref.watch(selectedDayProvider);
    if (day == null) {
      return const Center(child: Text('Select a day'));
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            DateFormat('EEEE, d MMMM yyyy').format(day.date),
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          Text(
            '${day.phase.emoji} ${day.phase.displayName} (${day.angle.toStringAsFixed(1)}°)',
            style: const TextStyle(fontSize: 15),
          ),
          if (day.isNewYear) ...[
            const SizedBox(height: 8),
            const Text(
              '🎇 Nisan 1 — Head of the Year (Rosh HaShanah)',
              style: TextStyle(
                color: AppTheme.newYearColor,
                fontWeight: FontWeight.bold,
                fontSize: 15,
              ),
            ),
          ],
          if (day.isNewMoon) ...[
            const SizedBox(height: 8),
            const Text(
              '🌑 New Moon — start of lunar month',
              style: TextStyle(
                color: AppTheme.newMoonColor,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
          if (day.isSabbath) ...[
            const SizedBox(height: 8),
            const Text(
              '🕊️ Sabbath — day of rest',
              style: TextStyle(color: AppTheme.sabbathColor),
            ),
          ],
          if (day.feast != null) ..._buildFeast(day),
        ],
      ),
    );
  }

  List<Widget> _buildFeast(CalendarDay day) {
    final feast = day.feast!;
    return [
      const SizedBox(height: 12),
      Text(
        '🎉 ${feast.name}',
        style: const TextStyle(
          color: AppTheme.feastColor,
          fontSize: 16,
          fontWeight: FontWeight.bold,
        ),
      ),
      if (feast.description != null) ...[
        const SizedBox(height: 4),
        Text(feast.description!, style: const TextStyle(fontSize: 14)),
      ],
      if (feast.bibleRefs.isNotEmpty) ...[
        const SizedBox(height: 8),
        ScriptureAccordion(refs: feast.bibleRefs),
      ],
    ];
  }
}
