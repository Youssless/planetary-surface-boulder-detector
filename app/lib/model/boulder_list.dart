
class BoulderList {
  final List<dynamic> boulders;

  BoulderList({required this.boulders});

  factory BoulderList.fromJson(Map<String, dynamic> json) {
    return BoulderList(
      boulders: json['data']
    );
  }
}