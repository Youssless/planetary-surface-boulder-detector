import 'package:flutter/material.dart';

class SideNavbar extends StatefulWidget {

  @override
  _SideNavbar createState() => new _SideNavbar();
}

class _SideNavbar extends State<SideNavbar> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return new NavigationRail(
      backgroundColor: Theme.of(context).primaryColorDark,
      selectedIndex: _selectedIndex,
      onDestinationSelected: (int index) {
        setState(() {
          _selectedIndex = index; 
        });
      },
      destinations: [
        NavigationRailDestination(
          icon: Icon(
            Icons.arrow_right_rounded,
            color: Theme.of(context).primaryColorLight,
            size: 75,
          ), 
          label: Text(
            "Run"
          )
        ),
        NavigationRailDestination(
          icon: Icon(
            Icons.edit,
            color: Theme.of(context).primaryColorLight,
          ),
          label: Text(
            "Edit"
          )
        )
      ], 
    );
  }
}