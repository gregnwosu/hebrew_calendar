import 'package:flutter/material.dart';

import '../models/calendar_day.dart';
import '../theme/app_theme.dart';

class DayCell extends StatelessWidget {
  const DayCell({
    super.key,
    required this.day,
    required this.isSelected,
    required this.onTap,
  });

  final CalendarDay day;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final badges = <String>[];
    if (day.isNewYear) badges.add('🎇');
    if (day.feast != null) badges.add('🎉');
    if (day.isSabbath) badges.add('🕊️');

    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          border: isSelected
              ? Border.all(color: AppTheme.selectedBorder, width: 2)
              : null,
          color: isSelected ? AppTheme.selectedBg : null,
          borderRadius: BorderRadius.circular(6),
        ),
        padding: const EdgeInsets.symmetric(vertical: 2, horizontal: 1),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              '${day.date.day}',
              style: TextStyle(
                fontSize: 13,
                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
              ),
            ),
            Text(day.phase.emoji, style: const TextStyle(fontSize: 14)),
            if (badges.isNotEmpty)
              Text(
                badges.join(' '),
                style: const TextStyle(fontSize: 10),
                overflow: TextOverflow.ellipsis,
              ),
          ],
        ),
      ),
    );
  }
}
