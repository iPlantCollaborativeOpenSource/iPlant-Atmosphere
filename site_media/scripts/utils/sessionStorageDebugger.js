var showAllSessionStorage=function(){sessionStorageValueSets={};for(i=0;i<=sessionStorage.length-1;i++)a=sessionStorage.key(i),pairs=sessionStorage.getItem(a),sessionStorageValueSets[a]=pairs;var c={},a=[],b=[];for(a in sessionStorageValueSets)sessionStorageValueSets.hasOwnProperty(a)&&b.push(a);b.sort();for(a=0;a<b.length;a++)c[b[a]]=sessionStorageValueSets[b[a]];for(property in c)console.log(property+" : "+sessionStorageValueSets[property])};
