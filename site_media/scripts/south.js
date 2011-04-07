/**
 *
 * Copyright (c) 2010, iPlant Collaborative, University of Arizona, Cold Spring Harbor Laboratories, University of Texas at Austin
 * This software is licensed under the CC-GNU GPL version 2.0 or later.
 * License: http://creativecommons.org/licenses/GPL/2.0/
 *
 * Author: Seung-jin Kim
 * Contact: seungjin@email.arizona.edu 
 * Twitter: @seungjin
 * 
 **/

var south = {
	init : new Ext.BoxComponent({
        region: 'south',
        height: 30, // give north and south regions a height
        autoEl: { tag: 'div', html:'<div id="footer"></div>' }
  })
};

