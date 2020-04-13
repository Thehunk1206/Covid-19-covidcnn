import 'dart:async';
import 'dart:io';


import 'package:tflite/tflite.dart';

import 'models/result.dart';


class TFLiteHelper {

  static StreamController<List<Result>> tfLiteResultsController = new StreamController.broadcast();
  static List<Result> _outputs = List();
  static var modelLoaded = false;

  static Future<String> loadModel() async{
    print("Loading model..");

    return Tflite.loadModel(
      model: "assets/covidcnn_161.tflite",
      labels: "assets/classes.txt",
    );
  }

  static classifyImage(File image) async {

    await Tflite.runModelOnImage(
        path: image.path,
        imageMean:0.0,
        imageStd: 255.0,
        threshold: 0.5,
            numResults: 1)
        .then((value) {
      if (value.isNotEmpty) {
        print("Results loaded. ${value.length}");

        //Clear previous results
        _outputs.clear();

        value.forEach((element) {
          _outputs.add(Result(
              element['confidence'], element['index'], element['label']));

          print("${element['confidence']} , ${element['index']}, ${element['label']}");
        });
      }

      //Sort results according to most confidence
      _outputs.sort((a, b) => a.confidence.compareTo(b.confidence));

      //Send results
      tfLiteResultsController.add(_outputs);
    });
  }

  static void disposeModel(){
    Tflite.close();
    tfLiteResultsController.close();
  }
}
