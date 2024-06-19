const dict = {
            1:["Test1.py", "10mb", "complete", "file"],
            2:["Test2.py", "20mb", "complete", "folder"],
            3:["Test3.py", "30mb", "complete", "file"],
            4:["Test4.py", "40mb", "complete", "folder"],
            5:["Test5.py", "50mb", "complete", "file"],
            6:["Test6.py", "60mb", "complete", "folder"],
            7:["Test7.py", "70mb", "complete", "file"],
            8:["Test8.py", "80mb", "complete", "folder"],
            9:["Test9.py", "90mb", "complete", "file"],
            10:["Tes10.py", "100mb", "complete", "folder"],
        };
var files = {};
var folders = {};
var fiFlag = 1;
var foFlag = 1;

for (const [key, value] of Object.entries(dict)){
    if (value[3] === "file"){
        files[fiFlag] = value;
        fiFlag += 1;
    }
    else if (value[3] === "folder"){
        folders[foFlag] = value;
        foFlag += 1;
    }
}

var fileWrapper = document.getElementById("accordionFile");
var folderWrapper = document.getElementById("accordionFolder");

var myFileHTML = '';
var myFolderHTML = '';

flag = 1
for (const [keyFile, valueFile] of Object.entries(files)) {
    myFileHTML += '<div class="accordion-item">\n' +
        '                <h2 class="accordion-header" id="heading'+flag+'">\n' +
        '                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse'+flag+'" aria-expanded="false" aria-controls="collapse'+flag+'">\n' +
        '                   '+valueFile[0]+'\n' +
        '                  </button>\n' +
        '                </h2>\n' +
        '                <div id="collapse'+flag+'" class="accordion-collapse collapse" aria-labelledby="heading'+flag+'" data-bs-parent="#accordionFile">\n' +
        '                  <div class="accordion-body text-dark">\n' +
        '                      <button type="button" class="btn btn-primary" value="'+valueFile[0]+' Download'+'">Download From Discord</button>\n' +
        '                      <button type="button" class="btn btn-primary" value="'+valueFile[0]+' Delete'+'">Delete From Discord</button>\n' +
        '                  </div>\n' +
        '                </div>\n' +
        '              </div>\n';
    flag += 1
}

for (const [keyFile, valueFile] of Object.entries(folders)) {
    myFolderHTML += '<div class="accordion-item">\n' +
        '                <h2 class="accordion-header" id="heading'+flag+'">\n' +
        '                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse'+flag+'" aria-expanded="false" aria-controls="collapse'+flag+'">\n' +
        '                   '+valueFile[0]+'\n' +
        '                  </button>\n' +
        '                </h2>\n' +
        '                <div id="collapse'+flag+'" class="accordion-collapse collapse" aria-labelledby="heading'+flag+'" data-bs-parent="#accordionFolder">\n' +
        '                  <div class="accordion-body text-dark">\n' +
        '                      <button type="button" class="btn btn-primary" value="noupload">Open Folder</button>\n' +
        '                      <button type="button" class="btn btn-primary" value="noupload">Delete Folder</button>\n' +
        '                  </div>\n' +
        '                </div>\n' +
        '              </div>\n';
    flag += 1
}

fileWrapper.innerHTML = myFileHTML;
folderWrapper.innerHTML = myFolderHTML;