/* Copyright (c) 2020 Wi-Fi Alliance */

/* Permission to use, copy, modify, and/or distribute this software for any / / purpose with or without fee is hereby granted, provided that the above / / copyright notice and this permission notice appear in all copies. */

/* THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL / / WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED / / WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL / / THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR / / CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING / / FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF / / CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT / / OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS / / SOFTWARE. */

------------------------------------------------------------------------
Run
------------------------------------------------------------------------
STAUT:  
sudo python3 ./app.py  
sudo python3 ./app.py \--interface &lt;wlan_interface&gt;  
APUT:  
sudo python3 ./app.py \--interface 2:&lt;if_name in 2.4G&gt;,2:&lt;if_name1 in 2.4G&gt;  
sudo python3 ./app.py \--interface 2:&lt;if_name in 2.4G&gt;,5:&lt;if_name in 5G&gt; <br />

------------------------------------------------------------------------
Extension/Modification Guide
------------------------------------------------------------------------
API class should not need to be modified because API only check/save TLV.  
To modify implementation in helper functions: inherit class  
ApCommandHelper, StaCommandHelper, CommandHelper and override original  
method. Use the naming of child class for new ap_command_helper,  
sta_command_helper, command_helper during importing.  

For example: Add New_ApCommandHelper in new_ap_command_helper.py  
Change this line in ap_commands.py:  
```
from .XXX_ap_command_helper import XXX_ApCommandHelper as ApCommandHelper
```
to:  
```
from .new_ap_command_helper import New_ApCommandHelper as ApCommandHelper
```
