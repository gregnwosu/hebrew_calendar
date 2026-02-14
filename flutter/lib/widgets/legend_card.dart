import 'package:flutter/material.dart';

class LegendCard extends StatelessWidget {
  const LegendCard({super.key});

  static const _items = [
    ('🌑', 'New Moon'),
    ('🌓', 'First Quarter'),
    ('🌕', 'Full Moon'),
    ('🌗', 'Third Quarter'),
    (null, null), // divider
    ('🎉', 'Feast Day'),
    ('🕊️', 'Sabbath'),
    ('🎇', 'New Year (Nisan 1)'),
  ];

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Legend',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            ..._items.map((item) {
              if (item.$1 == null) return const Divider();
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 3),
                child: Row(
                  children: [
                    Text(item.$1!, style: const TextStyle(fontSize: 16)),
                    const SizedBox(width: 8),
                    Text(item.$2!, style: const TextStyle(fontSize: 14)),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}
