import 'package:flutter/material.dart';

class AppTheme {
  AppTheme._();

  static const background = Color(0xFF222222);
  static const surface = Color(0xFF2D2D2D);
  static const selectedBorder = Color(0xFFffc107);
  static const selectedBg = Color(0x26ffc107);
  static const feastColor = Color(0xFF75b798);
  static const sabbathColor = Color(0xFF6ea8fe);
  static const newMoonColor = Color(0xFF17a2b8);
  static const newYearColor = Color(0xFFffc107);

  static ThemeData dark() {
    return ThemeData(
      brightness: Brightness.dark,
      scaffoldBackgroundColor: background,
      colorScheme: const ColorScheme.dark(
        surface: surface,
        primary: selectedBorder,
      ),
      cardTheme: const CardThemeData(
        color: surface,
        elevation: 2,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: background,
        elevation: 0,
      ),
      expansionTileTheme: const ExpansionTileThemeData(
        collapsedIconColor: Colors.white70,
        iconColor: selectedBorder,
      ),
    );
  }
}
