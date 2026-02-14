import 'package:flutter/material.dart';

import 'screens/calendar_screen.dart';
import 'theme/app_theme.dart';

class HebrewCalendarApp extends StatelessWidget {
  const HebrewCalendarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hebrew Calendar',
      theme: AppTheme.dark(),
      debugShowCheckedModeBanner: false,
      home: const CalendarScreen(),
    );
  }
}
