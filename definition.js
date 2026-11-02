// 1. Khối đọc chữ đã nhấn (Hình bầu dục - Output dạng Value để gán vào Biến)
Blockly.Blocks["touchpad_checkkeypad"] = {
  init: function() {
    this.jsonInit({
      "type": "touchpad_checkkeypad",
      "message0": Blockly.Msg.TOUCHPAD_CHECKKEYPAD_MESSAGE0,
      "output": null,
      "colour": "#e63022",
      "tooltip": Blockly.Msg.TOUCHPAD_CHECKKEYPAD_TOOLTIP,
      "helpUrl": Blockly.Msg.TOUCHPAD_CHECKKEYPAD_HELPURL
    });
  }
};

Blockly.Python["touchpad_checkkeypad"] = function(block) {
  Blockly.Python.definitions_["import_yolobit"] = "from yolobit import *";
  Blockly.Python.definitions_["import_keypad121"] = "from keypad121 import keypad";
  var code ="keypad.read()";
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// 2. Khối lệnh Xóa bộ nhớ (Có ngàm trên/dưới để ráp vào logic Nếu/Thì)
Blockly.Blocks['touchpad_clear'] = {
  init: function() {
    this.jsonInit({
      "type": "touchpad_clear",
      "message0": Blockly.Msg.TOUCHPAD_CLEAR_MESSAGE0,
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#e63022",
      "tooltip": Blockly.Msg.TOUCHPAD_CLEAR_TOOLTIP,
      "helpUrl": ""
    });
  }
};

Blockly.Python['touchpad_clear'] = function(block) {
  Blockly.Python.definitions_["import_yolobit"] = "from yolobit import *";
  Blockly.Python.definitions_["import_keypad121"] = "from keypad121 import keypad";
  return "keypad.clear()\n";
};