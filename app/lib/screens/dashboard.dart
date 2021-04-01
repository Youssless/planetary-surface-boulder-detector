import 'package:flutter/material.dart';
import 'package:app/widgets/side_navbar.dart';
import 'package:filepicker_windows/filepicker_windows.dart';

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
      alignment: Alignment.centerLeft,
      padding: EdgeInsets.all(20),
      child: new LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          return new Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              Text(
                "Dashboard"
              ),
              Spacer(flex: 6,),
              Text(
                "Processing"
              ),
              SizedBox(
                width: constraints.maxWidth*0.9,
                child: DropdownButtonFormField(
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
                )
              ),
              Spacer(flex: 2,),
              Text(
                "Input Image"
              ),
              SizedBox(
                width: constraints.maxWidth*0.9,
                child: TextFormField(
                  controller: TextEditingController(
                    text: _path
                  ),
                  readOnly: true,
                  decoration: InputDecoration(
                    //border: InputBorder.none,
                    hintText: 'Image path',
                    suffixIcon: IconButton(
                      icon: Icon(Icons.folder),
                      onPressed: () {
                        setFilePath();
                      },
                    )
                  ),
                ),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: constraints.maxWidth*0.45,
                    child: TextFormField(
                      decoration: InputDecoration(
                        //border: InputBorder.none,
                        hintText: 'width (pixels)',
                      ),
                    ),
                  ),
                  SizedBox(
                    width: constraints.maxWidth*0.45,
                    child: TextFormField(
                      decoration: InputDecoration(
                        //border: InputBorder.none,
                        hintText: 'height (pixels)',
                      ),
                    ),
                  ),
                ],
              ),
              
              Spacer(flex: 2,),
              Text(
                "Surface Model"
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: constraints.maxWidth*0.45,
                    child: TextFormField(
                      decoration: InputDecoration(
                        //border: InputBorder.none,
                        hintText: 'width (pixels)',
                      ),
                    ),
                  ),
                  SizedBox(
                    width: constraints.maxWidth*0.45,
                    child: TextFormField(
                      decoration: InputDecoration(
                        //border: InputBorder.none,
                        hintText: 'height (pixels)',
                      ),
                    ),
                  ),
                ],
              ),
              Spacer(flex: 3,),
              SizedBox(
                width: constraints.maxWidth*0.9,
                height: 50,
                child: ElevatedButton(
                  onPressed: () {
                    
                  }, 
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text("Run")
                    ],
                  )
                ),
              ),
              Spacer(flex: 12,)
            ],
          );
        },
      )
    );
  }

  void setFilePath() {
    final file = OpenFilePicker()
      ..filterSpecification = {
        "Image Files (*.jpg; *.jpeg; *.png)": "*.jpg;*.jpeg;*.png",
      }
      ..title = "Select an image";
    
    final result = file.getFile();
    if (result != null) {
      print(result.path);
      setState(() {
        _path = result.path;
      });
    }
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