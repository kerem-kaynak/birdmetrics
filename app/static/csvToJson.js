let data_arr = {}
const uploadButton = document.getElementById('uploadButton').addEventListener('click', () => {
    Papa.parse(document.getElementById('fileUpload').files[0],
    {
        download:true,
        header:false,
        skipEmptyLines:true,
        complete: function(results){
            for(let i = 0; i < results.data.length; i++){
                let temp = results.data[i].filter(element => {
                    return element !== '';
                  });
                temp.splice(0,1)
                data_arr[results.data[i][0]] = temp
            }
            
            $.post( "/upload", {
                data: JSON.stringify(data_arr) 
            });
        }
    })
})