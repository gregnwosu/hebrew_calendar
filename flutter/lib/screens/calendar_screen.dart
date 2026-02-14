import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/calendar_providers.dart';
import '../widgets/calendar_grid.dart';
import '../widgets/day_detail_panel.dart';
import '../widgets/legend_card.dart';
import '../widgets/month_navigation.dart';

class CalendarScreen extends ConsumerStatefulWidget {
  const CalendarScreen({super.key});

  @override
  ConsumerState<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends ConsumerState<CalendarScreen> {
  final _focusNode = FocusNode();

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  void _onKey(KeyEvent event) {
    if (event is! KeyDownEvent) return;

    int delta = 0;
    if (event.logicalKey == LogicalKeyboardKey.arrowRight) {
      delta = 1;
    } else if (event.logicalKey == LogicalKeyboardKey.arrowLeft) {
      delta = -1;
    } else if (event.logicalKey == LogicalKeyboardKey.arrowDown) {
      delta = 7;
    } else if (event.logicalKey == LogicalKeyboardKey.arrowUp) {
      delta = -7;
    }
    if (delta == 0) return;

    final current = ref.read(selectedDateProvider);
    final next = current.add(Duration(days: delta));
    ref.read(selectedDateProvider.notifier).state = next;

    // Update month view if we crossed a month boundary
    final viewMonth = ref.read(currentMonthProvider);
    if (next.year != viewMonth.year || next.month != viewMonth.month) {
      ref.read(currentMonthProvider.notifier).state =
          DateTime(next.year, next.month);
    }
  }

  void _onSwipe(DragEndDetails details) {
    if (details.primaryVelocity == null) return;
    final current = ref.read(currentMonthProvider);
    if (details.primaryVelocity! < -200) {
      // Swipe left → next month
      _goMonth(current, 1);
    } else if (details.primaryVelocity! > 200) {
      // Swipe right → prev month
      _goMonth(current, -1);
    }
  }

  void _goMonth(DateTime current, int delta) {
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

  @override
  Widget build(BuildContext context) {
    final dataAsync = ref.watch(calendarDataProvider);

    return dataAsync.when(
      loading: () => const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      ),
      error: (e, _) => Scaffold(
        body: Center(child: Text('Error loading data: $e')),
      ),
      data: (_) => KeyboardListener(
        focusNode: _focusNode,
        autofocus: true,
        onKeyEvent: _onKey,
        child: Scaffold(
          appBar: AppBar(
            title: const Text('🌙 Hebrew Calendar'),
            centerTitle: true,
          ),
          body: LayoutBuilder(
            builder: (context, constraints) {
              if (constraints.maxWidth >= 800) {
                return _wideLayout();
              }
              return _narrowLayout();
            },
          ),
        ),
      ),
    );
  }

  Widget _narrowLayout() {
    return GestureDetector(
      onHorizontalDragEnd: _onSwipe,
      child: ListView(
        padding: const EdgeInsets.all(12),
        children: const [
          _InfoBanner(),
          SizedBox(height: 8),
          Card(child: _CalendarSection()),
          SizedBox(height: 12),
          Card(child: DayDetailPanel()),
          SizedBox(height: 12),
          LegendCard(),
          SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _wideLayout() {
    return GestureDetector(
      onHorizontalDragEnd: _onSwipe,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 3,
            child: ListView(
              padding: const EdgeInsets.all(12),
              children: const [
                _InfoBanner(),
                SizedBox(height: 8),
                Card(child: _CalendarSection()),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: ListView(
              padding: const EdgeInsets.all(12),
              children: const [
                Card(child: DayDetailPanel()),
                SizedBox(height: 12),
                LegendCard(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoBanner extends StatelessWidget {
  const _InfoBanner();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF17a2b8).withAlpha(30),
        borderRadius: BorderRadius.circular(8),
      ),
      child: const Text(
        '🌙 Feasts and Sabbaths begin at sunset on the date shown (evening to evening)',
        textAlign: TextAlign.center,
        style: TextStyle(fontSize: 13),
      ),
    );
  }
}

class _CalendarSection extends StatelessWidget {
  const _CalendarSection();

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(12),
      child: Column(
        children: [
          MonthNavigation(),
          SizedBox(height: 8),
          CalendarGrid(),
        ],
      ),
    );
  }
}
