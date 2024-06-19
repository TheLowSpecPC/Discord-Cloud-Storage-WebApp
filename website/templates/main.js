fetch('/fetch').then(response => response.json()).then(function (data){
    var files = {};
    var folders = [];

    for (const [key, value] of Object.entries(data)){
        if (value[1] === "null"){
            files[key] = value;
        }
        else{
            if (folders.indexOf(value[1]) === -1){
                folders.push(value[1]);
            }
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
            '                   '+keyFile+' Size:'+valueFile[0]+'\n' +
            '                  </button>\n' +
            '                </h2>\n' +
            '                <div id="collapse'+flag+'" class="accordion-collapse collapse" aria-labelledby="heading'+flag+'" data-bs-parent="#accordionFile">\n' +
            '                  <div class="accordion-body text-dark">\n' +
            '                      <button type="button" class="btn btn-primary" onclick="clickResponse(this)" value="'+keyFile+' Download'+'">Download From Discord</button>\n' +
            '                      <button type="button" class="btn btn-primary" onclick="clickResponse(this)" value="'+keyFile+' Delete'+'">Delete From Discord</button>\n' +
            '                  </div>\n' +
            '                </div>\n' +
            '              </div>\n';
        flag += 1
    }

    for (const keyFile of folders) {
        console.log(keyFile)
        myFolderHTML += '<div class="accordion-item">\n' +
            '                <h2 class="accordion-header" id="heading'+flag+'">\n' +
            '                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse'+flag+'" aria-expanded="false" aria-controls="collapse'+flag+'">\n' +
            '                   '+keyFile+'\n' +
            '                  </button>\n' +
            '                </h2>\n' +
            '                <div id="collapse'+flag+'" class="accordion-collapse collapse" aria-labelledby="heading'+flag+'" data-bs-parent="#accordionFolder">\n' +
            '                  <div class="accordion-body text-dark">\n' +
            '                      <button type="button" class="btn btn-primary" onclick="clickResponse(this)" value="'+keyFile+' Open'+'">Open Folder</button>\n' +
            '                      <button type="button" class="btn btn-primary" onclick="clickResponse(this)" value="'+keyFile+' Delete'+'">Delete Folder</button>\n' +
            '                  </div>\n' +
            '                </div>\n' +
            '              </div>\n';
        flag += 1
    }

    fileWrapper.innerHTML = myFileHTML;
    folderWrapper.innerHTML = myFolderHTML;
})

function clickResponse(btn) {
        alert(btn.value)
    }