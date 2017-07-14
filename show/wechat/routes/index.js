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

            fcb(chosen_fund);
        });

        db.close();
    });
  };
  
}).call(this);

var findDocuments = function(db, fcb) {
  // Get the documents collection 
  var chosen_fund_set = db.collection('chosen_fund_set');
  // Find some documents 
  chosen_fund_set.find({}).toArray(function(err, rows) {
    assert.equal(err, null);
    //assert.equal(2, docs.length);
    console.log("findDocuments:get rows sucessfully");
    fcb(rows);
  });
}