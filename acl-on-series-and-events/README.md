# ACL on Series and Events

Collection of scripts dealing with ACLs on Series and Events using
the API.

Target audience: Opencast system administrators.

## src/migrate_roles.js

Copy Access-Control-List (ACL) rules of Series and Events matching
`ROLE_PATTERN` to `ROLE_COPY` using the External API using a browser's
Web Console.

### The User Story
There were about 3000 Events and 300 Series in an Opencast installation
that needed their Role-Prefix in ACLs changed due to the way Opencast
has been integrated in ILIAS. Published Events needed their meta data
republished in Engage. The process should take place during normal
operations (visitors watching videos, lectures being recorded, recordings
being processed) without too much impact on user experience.

### Usage
1. Adjust the constants on top of this script according to your setup.
2. Open your Opencast Admin interface in a compatible browser, log in,
   and navigate to your REST-API docs. By default, they are located at
   `/rest_docs.html`
3. Open your Browser's web console and the network tab. Make logging
   persistent. Switch to the console tab.
4. Copy your modified version of the script into the clipboard, paste
   its contents to the browser's console and hit enter.
5. The script starts to run. You can interrupt the script at any time
   by reloading the page.
6. You can inspect the HTTP requests to the External API, switching to
   your browser's network tab.
7. When the script has finished, it says "done" in your browser console.
8. Since the script will not write anything to the API if there were no
   changes and the script will also avoid adding duplicate rules, the
   script can be run multiple times, for instance if some events or series
   could not be changed due to Workflows running on them.

### Compatibility
Makes use of Public field declarations in Classes as proposed at TC39,
the JavaScript standards committee. Tested in Mozilla Firefox 72.
https://github.com/tc39/proposal-class-fields
Makes use of jQuery for AJAX-Requests, which is shipped with Opencast.

### Limitations
The script does not yet support pagination. All Events and Series are
obtained, up to a limit or none, at once. This may not cover all your
Events/Series in Opencast or may crash your browser if the list is too
huge.
