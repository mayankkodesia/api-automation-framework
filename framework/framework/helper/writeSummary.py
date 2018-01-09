'''
Created on 10-Jun-2014
@author: Mayank Kodesia
'''

import os
def writeStyle(f):
    string = '''<style type="text/css" media="screen">
                .trrr{
                
                background-color: lightblue;
                /*height: 500px;*/
                width: 500px;
    
                }
                .trr{
                
                background-color: lightblue;
                height: 50px;
                width: 50px;
    
                }
                </style>'''
    f.write(string)

def main(reportDir=""):
    finalDigit=0
    passed = 0
    failed = 0
    moreThan2 = 0

    relative =  os.path.dirname(__file__) + "/../report/" + reportDir + "/"
    if os.path.exists(relative+"summary.html"):
#         os.system("rm -f "+relative+"summary.html")
        os.remove(relative+"summary.html")
        
    # if os.path.exists(relative+"ErrorCount.html"):
    #     os.system("rm -f "+relative+"ErrorCount.html")
    
    errorList = []
    urlList = []
    urlDict = {}
    
    for root, subFolders, files in os.walk(relative):
        if 'external' in root or 'logs' in root or 'failed' in root:
            pass
        else:
            for f in files:
                if  str(f).endswith(".html"):
    #                 print(f)
                    with open(os.path.join(root,f), 'r') as fil:
                        for lines in fil:
                            if "Total Test Cases in All suites" in lines:
                                digit = str(lines).strip().split("=")[1].strip()
                                finalDigit += int(digit.strip())
                            
                            if "Passed Test cases in All suites" in lines:
                                passe = str(lines).strip().split("=")[1].strip()
                                passed += int(passe.strip())
                                
                            if "Failed Test cases in All suites" in lines:
                                faile = str(lines).strip().split("=")[1].strip()
                                failed += int(faile.strip())
                                
                            if "Test cases took more than" in lines:
                                moreThan2Sec = str(lines).strip().split("=")[1].strip()
                                moreThan2 += int(moreThan2Sec.strip())
    
    
                    with open(os.path.join(root,f), 'r') as fil:
                        data=fil.read().replace('\n', '')
    #                     print data
                        import re
                        while "<tr>" in data and "</tr>" in data :
                            r = re.compile('<tr>(.*?)</tr>')
                            m = r.search(data)
                            if m:
                                row = m.group()
                                if 'FAILED' in row:
                                    newRow = row.replace("<tr>", "").replace("</tr>", "")
                                    pattern = re.compile("<td(.*?)</td>")
                                    tdList = re.findall(pattern, newRow)
#                                     expected = re.findall(re.compile("</div>(.*?)</div>"), tdList[-1])[0]
#                                     url = tdList[2].replace(">", "")
#                                     key = expected.partition("Actual Response")[0]+ "<b>URL</b>: "+ url.split("?")[0]
#                                     errorList.append(key)
    #                                 urlList.append(url)
#                                     if urlDict.has_key(key):
#                                         urlDict.get(key).append(url)
#                                     else:
#                                         urlDict[key]=[url]
                                data = data.replace(row, "")
    
                        
    with open(relative+"summary.html", "w") as f:
        f.write("<html><body bgcolor=#E6E6FA>")
        f.write("<pre><b>**********Results Summary For Executed Build********<br/><br/></b>")
        f.write("Total Test Cases in All suites  =  "+ str(finalDigit).strip() + "<br/>")
        f.write("<font color=green>Passed Test cases in All suites = "+str(passed) +"<br/></font>")
        f.write("<b><font color=red>Failed Test cases in All suites = "+str(failed)+"<br/></font></b>")
    #     f.write("<b>Test Cases took more than 2 sec in All suites  = "+str(moreThan2)+"<br/><br/></font></b>")
        f.write("****************************************************")
        f.write("</pre></body></html>")
        f.close()



# with open(relative+"ErrorCount.html", "a") as f:
#     f.write("<html><body bgcolor=#E6E6FA>")
#     writeStyle(f)
#     f.write("<pre><b>**********Results Summary For Executed Build********<br/><br/></b>")
#     f.write("Total Test Cases in All suites  =  "+ str(finalDigit).strip() + "<br/>")
#     f.write("<font color=green>Passed Test cases in All suites = "+str(passed) +"<br/></font>")
#     f.write("<b><font color=red>Failed Test cases in All suites = "+str(failed)+"<br/></font></b>")
#     f.write("<b>Test Cases took more than 2 sec in All suites  = "+str(moreThan2)+"<br/><br/></font></b>")
#     f.write("****************************************************")
# 
#     
#     f.write("<pre><b>**********Error Summary For Executed Build********<br/><br/></b>")
#     f.write("<table border=1>")
#     
#     for key in list(set(errorList)):
#         f.write("<tr border=1>")
#         f.write('<td class="trrr" border=1 align="left">')
#         f.write(key + "<br/>" + " <br/>".join(urlDict.get(key)))
#         f.write("</td>")
#         
#         f.write('<td class="trr" border=1 align="center">')
#         f.write(str(errorList.count(str(key))))
#         f.write("</td>")
# #         
#         f.write("</tr>")
#         
#     f.write("</table>")
#     f.write("</html>")
#     f.close()
