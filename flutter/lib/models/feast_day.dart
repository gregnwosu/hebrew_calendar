class FeastDay {
  const FeastDay({
    required this.name,
    this.description,
    this.bibleRefs = const [],
  });

  final String name;
  final String? description;
  final List<String> bibleRefs;

  factory FeastDay.fromJson(Map<String, dynamic> json) {
    return FeastDay(
      name: json['name'] as String,
      description: json['description'] as String?,
      bibleRefs: (json['bibleRefs'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
    );
  }
}
