__author__ = 'LT-CSIN'


class HTMLWriter(object):
    '''
    This class is used to write HTML code and java script in
    final report
    '''

    def __init__(self):
        pass

    def write_show_hide_inHTML(self, File):
        File.write('''
                    function show(label)
                        {
                            fail_reason = document.getElementById("input_" + label).value
                            document.getElementById(label).innerHTML=fail_reason;
                        }

                    function hide(label, fail_reason)
                        {
                            document.getElementById(label).innerHTML="";
                        }
                      ''')


    def write_css(self,File):
        File.write('''
            <style type="text/css" media="screen">
            .popup_window {
            display: none;
            position: relative;
            left: 0px;
            top: 0px;
            /*border: solid #627173 1px; */
            padding: 10px;
            background-color: #81BEF7;
            font-family: "Lucida Console", "Courier New", Courier, monospace;
            text-align: left;
            font-size: 8pt;
            width: 500px;}
            </style>
            ''')


    def startJavaScript(self, File):
        File.write('''<script>''')

    def endJavaScript(self, File):
        File.write('''</script>''')


    def showTestDetail(self, File):
        File.write('''
            function showTestDetail(div_id){
            var details_div = document.getElementById(div_id)
            var displayState = details_div.style.display
            // alert(displayState)
            if (displayState != 'block' ) {
                displayState = 'block'
                details_div.style.display = 'block'
            }
            else {
                details_div.style.display = 'none'
            }
        }''')

