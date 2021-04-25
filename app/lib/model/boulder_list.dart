
class BoulderList {
  final String outImagePath;
  final List<dynamic> boulders;

  BoulderList({required this.outImagePath, required this.boulders});

  factory BoulderList.fromJson(Map<String, dynamic> json) {
    return BoulderList(
      outImagePath: json['data']['out_img'],
      boulders: json['data']['boulder_list']
    );
  }
}