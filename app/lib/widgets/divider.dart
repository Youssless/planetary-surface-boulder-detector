import 'package:flutter/material.dart';


class TextDivider extends StatelessWidget {
  final double indent;
  final String text;

  TextDivider({required this.text, required this.indent});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: <Widget>[
        Expanded(
          child: Divider(
            height: 1,
            indent: indent,
            endIndent: indent,
            thickness: 1,
          ),
        ),
          

          Text(text, 
            style: TextStyle(
              color: Colors.grey
            ),
          ),        

          Expanded(
              child: Divider(
                height: 1,
                indent: indent,
                endIndent: indent,
                thickness: 1,
              )
          ),
      ]
    );
  }
}