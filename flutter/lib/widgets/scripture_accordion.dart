import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/calendar_providers.dart';

class ScriptureAccordion extends ConsumerWidget {
  const ScriptureAccordion({super.key, required this.refs});

  final List<String> refs;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final repo = ref.watch(calendarRepositoryProvider);
    if (repo == null) return const SizedBox.shrink();

    return Column(
      children: refs.map((r) {
        final text = repo.getScripture(r) ?? '';
        return ExpansionTile(
          title: Text(r, style: const TextStyle(fontSize: 14)),
          tilePadding: EdgeInsets.zero,
          childrenPadding: const EdgeInsets.only(bottom: 12),
          children: [
            Text(
              text,
              style: const TextStyle(fontSize: 13, height: 1.5),
            ),
          ],
        );
      }).toList(),
    );
  }
}
