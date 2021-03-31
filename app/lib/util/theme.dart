import 'package:flutter/material.dart';



final ThemeData DefaultTheme = new ThemeData(
  primaryColorLight: DefaultColors.BlueNCS[300],
  primaryColorDark: DefaultColors.EagleGreen[400],

);

class DefaultColors {
  static const Map<int, Color> EagleGreen = const <int, Color> {
    400: const Color(0xFF073B4C)
  };

  static const Map<int, Color> BlueNCS = const <int, Color> {
    300: const Color(0xFF1FB7EA),
    400: const Color(0xFF118AB2)
  };

  static const Map<int, Color> ImperialRed = const <int, Color> {
    400: const Color(0xFFE63946)
  };
}