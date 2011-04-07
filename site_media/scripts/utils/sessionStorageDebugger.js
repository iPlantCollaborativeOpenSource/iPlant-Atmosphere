var showAllSessionStorage = function() {
  
  sessionStorageValueSets = {};
  for (i=0;i<=sessionStorage.length-1;i++) {
    key = sessionStorage.key(i);
				pairs = sessionStorage.getItem(key);
				//console.log(key + " : " + pairs)
    sessionStorageValueSets[key] = pairs;
		};
  
  //return sessionStorageValueSets;
  //console.log(sessionStorageValueSets);
  
  // sorting block starts
  var sorted = {};
  key, a = [];
  for (key in sessionStorageValueSets) {
    if (sessionStorageValueSets.hasOwnProperty(key)) {
                a.push(key);
        }
  }
  a.sort();
  for (key = 0; key < a.length; key++) {
        sorted[a[key]] = sessionStorageValueSets[a[key]];
  }
  //sorting block ends
  
  for ( property in sorted ) console.log(property + " : " + sessionStorageValueSets[property]);


};