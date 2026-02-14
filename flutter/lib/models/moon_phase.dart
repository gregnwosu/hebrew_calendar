enum MoonPhase {
  newMoon('New Moon', '🌑'),
  waxingCrescent('Waxing Crescent', '🌒'),
  firstQuarter('First Quarter', '🌓'),
  waxingGibbous('Waxing Gibbous', '🌔'),
  fullMoon('Full Moon', '🌕'),
  waningGibbous('Waning Gibbous', '🌖'),
  thirdQuarter('Third Quarter', '🌗'),
  waningCrescent('Waning Crescent', '🌘');

  const MoonPhase(this.displayName, this.emoji);

  final String displayName;
  final String emoji;

  static MoonPhase fromString(String name) {
    return MoonPhase.values.firstWhere(
      (p) => p.displayName == name,
      orElse: () => MoonPhase.newMoon,
    );
  }
}
