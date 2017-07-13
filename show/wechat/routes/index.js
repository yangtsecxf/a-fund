var db = require('mongodb');
var MongoClient = require('mongodb').MongoClient, assert = require('assert'); 


(function() {
  // fcb(chosen_fund)
  exports.getfund = function(msg, fcb) {
    reg = new RegExp('jj', 'i');
    if (reg.test(msg.content) === true) {     
    }

    // read db
    var url = 'mongodb://localhost:27017/fund';
    MongoClient.connect(url, function(err, db) {
        assert.equal(null, err);
        console.log("Connected correctly to server");
        
        // find mix4
        findDocuments(db, function(rows) { 
            console.log(rows.length);
            if (rows.length <= 0) {
                fcb("");
            }
              
            var index_last = rows.length > 0 ? rows.length - 1 : 0;      
            console.log(index_last);
            var chosen_fund = rows[index_last].mix4;
            console.log(resMsg);

            fcb(chosen_fund);
        });

        db.close();
    });
  };
  
}).call(this);

/*
//@ sourceMappingURL=index.map
*/
