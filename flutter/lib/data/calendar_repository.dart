import '../models/calendar_day.dart';
import 'calendar_data_loader.dart';

class CalendarRepository {
  CalendarRepository(this._data);

  final CalendarData _data;

  CalendarDay? getDay(DateTime date) {
    return _data.days[DateTime(date.year, date.month, date.day)];
  }

  List<CalendarDay?> getMonth(int year, int month) {
    final daysInMonth = DateTime(year, month + 1, 0).day;
    return List.generate(daysInMonth, (i) {
      return getDay(DateTime(year, month, i + 1));
    });
  }

  String? getScripture(String ref) {
    return _data.scriptures[ref];
  }

  bool hasData(DateTime date) {
    return _data.days.containsKey(DateTime(date.year, date.month, date.day));
  }
}
