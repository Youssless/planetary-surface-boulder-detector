import 'package:flutter/material.dart';
import 'package:app/widgets/side_navbar.dart';

class Home extends StatefulWidget {

  @override
  _Home createState() => new _Home();

}

class _Home extends State<Home> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      body: new Container(
        child: Row (
          children: [
            Expanded(
              flex: 2,
              child: SideNavbar(),
            ),
            Expanded(
              flex: 10,
              child: Dashboard()
            ),
            Expanded(
              flex: 20,
              child: ImageView()
            )
            
          ],
          
        ),
          
          //ImageView()
      )
    );
  }
}


class Dashboard extends StatefulWidget {

  @override
  _Dashboard createState() => new _Dashboard();
}

class _Dashboard extends State<Dashboard> {
  int? _value;
  String _path = "";

  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return new Container(
      alignment: Alignment.center,
      padding: EdgeInsets.all(20),
      child: new Column(
        children: <Widget>[
          Spacer(flex: 6,),
          SizedBox(
            width: 300,
            child: dropDownMenu(),
          ),
          Spacer(flex: 1,),
          SizedBox(
            width: 300,
            child: TextFormField(
              decoration: InputDecoration(
                //border: InputBorder.none,
                hintText: 'Image path',
              ),
            ),
          ),
          Spacer(flex: 1,),
          SizedBox(
            width: 300,
            child: TextFormField(
              decoration: InputDecoration(
                //border: InputBorder.none,
                hintText: 'Image size',
              ),
            ),
          ),
          Spacer(flex: 1,),
          SizedBox(
            width: 300,
            child: TextFormField(
              decoration: InputDecoration(
                //border: InputBorder.none,
                hintText: 'Surface model size ',
              ),
            ),
          ),
          Spacer(flex: 3,),
          SizedBox(
            width: 300,
            height: 50,
            child: ElevatedButton(
              onPressed: () {
                
              }, 
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text("Submit")
                ],
              )
            ),
          ),
          Spacer(flex: 12,)
        ],
      )
    );
  }

  Widget dropDownMenu() {
    return DropdownButtonFormField(
      value: _value,
      hint: Text("Processor"),
      items: [
        DropdownMenuItem(
          child: Text("CPU"),
          value: 0,
        ),
        DropdownMenuItem(
          child: Text("GPU"),
          value: 1,
        )
      ],
      onChanged: (int? value) {
        setState(() {
          _value = value;
        });
      },
    );
  }
}

class ImageView extends StatefulWidget {

  @override
  _ImageView createState() => new _ImageView();
}

class _ImageView extends State<ImageView> {

  @override
  Widget build(BuildContext context) {
    return new Container(
      child: new Row(
        children: [
        ],
      ),
    );
  }
}