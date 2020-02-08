/**
 * migrate_roles.js
 *
 * Copy Access-Control-List (ACL) rules of Series and Events matching
 * ROLE_PATTERN to ROLE_COPY using the External API using a browser's
 * Web Console.
 *
 * The story:
 * There were about 3000 Events and 300 Series in an Opencast installation
 * that needed their Role-Prefix in ACLs changed due to the way Opencast
 * has been integrated in ILIAS. Published Events needed their meta data
 * republished in Engage. The process should take place during normal
 * operations (visitors watching videos, lectures being recorded, recordings
 * being processed) without too much impact on user experience.
 *
 * Usage:
 * 1. Adjust the constants on top of this script according to your setup.
 * 2. Open your Opencast Admin interface in a compatible browser, log in,
 *    and navigate to your REST-API docs. By default, they are located at
 *    /rest_docs.html
 * 3. Open your Browser's web console and the network tab. Make logging
 *    persistent. Switch to the console tab.
 * 4. Copy your modified version of the script into the clipboard, paste
 *    its contents to the browser's console and hit enter.
 * 5. The script starts to run. You can interrupt the script at any time
 *    by reloading the page.
 * 6. You can inspect the HTTP requests to the External API, switching to
 *    your browser's network tab.
 * 7. When the script has finished, it says "done" in your browser console.
 * 8. Since the script will not write anything to the API if there were no
 *    changes and the script will also avoid adding duplicate rules, the
 *    script can be run multiple times, for instance if some events or series
 *    could not be changed due to Workflows running on them.
 *
 * Compatibility:
 * Makes use of Public field declarations in Classes as proposed at TC39,
 * the JavaScript standards committee. Tested in Mozilla Firefox 72.
 * https://github.com/tc39/proposal-class-fields
 * Makes use of jQuery for AJAX-Requests, which is shipped with Opencast.
 *
 * Limitations:
 * The script does not yet support pagination. All Events and Series are
 * obtained, up to a limit or none, at once. This may not cover all your
 * Events/Series in Opencast or may crash your browser if the list is too
 * huge.
 *
 * MIT License:
 * Copyright 2020 Felix Pahlow <https://wohlpa.de> - open source consulting
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 *
 * For support and updates you may contact https://wohlpa.de
 */
/* jshint esversion: 10, jquery: true*/
/* eslint-env es2020, browser, jquery */
(function(w, $) {
  'use strict';

  // Constants to adjust
  // /////////////////////////////////////////////////////////////
  // Workflow ID identifying the "Republish Metadata" Workflow
  const REPUBLISH_METADATA_WF = 'republish-metadata-llz';

  // Time to wait after a metadata republish WF has been instantiated
  // in ms. This is to avoid adding too much stress to the system.
  const REPUBLISH_SCHEDULE_DELAY = 6000;

  // Pattern to match all existing roles against
  const ROLE_PATTERN = /^ROLE_GROUP_(\d+)_LEARNER$/;

  // Replace to apply when a match in existing roles were found
  const ROLE_COPY = 'ILIAS_$1_LEARNER';
  // /////////////////////////////////////////////////////////////

  /**
   * Log message to console
   */
  function log(...messages) {
    console.log(...messages);
  }

  /**
   * Send warning message to console
   */
  function warn(...messages) {
    console.warn(...messages);
  }

  /**
   * Send error message to console
   */
  function error(...messages) {
    console.error(...messages);
  }

  /**
   * Catalogue of Series
   */
  class Series {
    apiResult = null;
    index = -1;
    length = -1;

    /**
     * @param {Array} apiResult
     */
    constructor(apiResult) {
      this.apiResult = apiResult;
      this.length = apiResult.length;
    }
    /**
     * Next Serie from the catalogue
     * @return {Serie}
     */
    next() {
      const serie = this.apiResult[++this.index];
      return new Serie(serie);
    }
    /**
     * Is there one more serie that wasn't returned by next?
     * @return {boolean}
     */
    hasNext() {
      return this.index < this.apiResult.length - 1;
    }
    /**
     * Load the series catalogue from API and resolve promise with
     * Series object when done.
     *
     * @return {$.Promise}
     */
    static fromApi() {
      const $deferred = new $.Deferred();

      $.get('/api/series/', {
        'limit': 50000, // default is 100 which is much too less
      }).done(function(r) {
        const series = new Series(r);
        log(series.length + ' series received.');
        $deferred.resolve(series);
      }).fail(function(r) {
        warn('GET /api/series/ failed.');
        $deferred.reject(r);
      });

      return $deferred.promise();
    }
  }
  /**
   * Single Series Object
   */
  class Serie {
    apiResult = null;
    id = undefined;

    /**
     * @param {Object} apiResult
     */
    constructor(apiResult) {
      this.apiResult = apiResult;
      this.id = apiResult.identifier;
    }
    /**
     * Fetch ACL (Access Control List) and resolve promise with Acl when done.
     *
     * @return {$.Promise}
     */
    getAcl() {
      const $deferred = new $.Deferred();
      const id = this.id;

      $.get('/api/series/' + id + '/acl').done(function(r) {
        const acl = new Acl(r);
        $deferred.resolve(acl);
      }).fail(function(r) {
        warn('GET /api/series/' + id + '/acl failed.');
        $deferred.reject(r);
      });

      return $deferred.promise();
    }
    /**
     * Put ACLs to server and resolve promise when done.
     *
     * @param {Acl} acl
     * @return {$.jqXHR}
     */
    setAcl(acl) {
      const $deferred = new $.Deferred();
      const id = this.id;

      $.ajax({
        method: 'PUT',
        url: '/api/series/' + id + '/acl',
        dataType: 'json',
        data: {
          'acl': acl.getJSON(),
        },
      }).done(function() {
        $deferred.resolve();
      }).fail(function(r) {
        warn('PUT /api/series/' + id + '/acl failed.');
        $deferred.reject(r);
      });

      return $deferred.promise();
    }
  }
  /**
   * An Access Control List (ACL)
   * An ACL specifies which role is allowed to (read|write)
   */
  class Acl {
    apiResult = null;

    /**
     * @param {Array} apiResult
     */
    constructor(apiResult) {
      this.apiResult = apiResult;
    }
    /**
     * @return {string} JSON representation of the ACL
     */
    getJSON() {
      return JSON.stringify(this.apiResult);
    }
    /**
     * @param {string} rule
     * @return {boolean}
     */
    contains(rule) {
      const len = this.apiResult.length;

      for (let i = 0; i < len; ++i) {
        const existingRule = this.apiResult[i];
        let matches = true;
        for (const key in existingRule) {
          if (existingRule.hasOwnProperty(key)) {
            matches = matches && existingRule[key] === rule[key];
          }
        }
        if (matches) return true;
      }
      return false;
    }
    /**
     * For each rule in the ACL, see if pattern matches against a role,
     * and if so, copy the rule, modified by replace if the rule is not
     * already in (avoids exact duplicate rules)
     * @param {RegExp} rolePattern
     * @param {string} roleReplace
     * @return {boolean} whether something was changed
     */
    duplicateRules(rolePattern, roleReplace) {
      let changesMade = false;
      const len = this.apiResult.length;

      for (let i = 0; i < len; ++i) {
        const rule = this.apiResult[i];
        if (rolePattern.test(rule.role)) {
          const copy = $.extend(true, {}, rule);
          copy.role = copy.role.replace(rolePattern, roleReplace);
          if (!this.contains(copy)) {
            log('Copy role: ' + rule.role + ' -> ' + copy.role);
            this.apiResult.push(copy);
            changesMade = true;
          }
        }
      }
      return changesMade;
    }
    /**
     * Remove a rule if the role matches the pattern provided
     * @param {RegExp} rolePattern
     */
    removeRules(rolePattern) {
      let i;
      const len = this.apiResult.length;
      const copy = [];
      for (i = 0; i < len; i++) {
        const rule = this.apiResult[i];
        if (!rule.role.test(rolePattern)) {
          copy.push(rule);
        }
      }
      this.apiResult = copy;
    }
  }
  /**
   * Catalogue of Events
   */
  class Events {
    apiResult = null;
    index = -1;
    length = -1;

    /**
     * @param {Array} apiResult
     */
    constructor(apiResult) {
      this.apiResult = apiResult;
      this.length = apiResult.length;
    }
    /**
     * Next Event/Episode from the catalogue
     * @return {Event}
     */
    next() {
      const event = this.apiResult[++this.index];
      return new Event(event);
    }
    /**
     * Is there one more event that wasn't returned by next?
     * @return {boolean}
     */
    hasNext() {
      return this.index < this.apiResult.length - 1;
    }
    /**
     * Load the event catalogue from API and resolve promise with
     * Events object when done.
     * @return {$.Promise}
     */
    static fromApi() {
      const $deferred = new $.Deferred();

      $.get('/api/events/').done(function(r) {
        const events = new Events(r);
        log(events.length + ' events received.');
        $deferred.resolve(events);
      }).fail(function(r) {
        warn('GET /api/events/ failed.');
        $deferred.reject(r);
      });

      return $deferred.promise();
    }
  }
  /**
   * Single Event Object
   */
  class Event {
    apiResult = null;
    id = undefined;
    isPublished = false;

    /**
     * @param {Object} apiResult
     */
    constructor(apiResult) {
      this.apiResult = apiResult;
      this.id = apiResult.identifier;
    }
    /**
     * Fetch ACL and resolve promise with Acl when done.
     * @return {$.Promise}
     */
    getAcl() {
      const $deferred = new $.Deferred();
      const id = this.id;

      $.get('/api/events/' + id + '/acl').done(function(r) {
        const acl = new Acl(r);
        $deferred.resolve(acl);
      }).fail(function(r) {
        warn('GET /api/events/' + id + '/acl failed.');
        $deferred.reject(r);
      });

      return $deferred.promise();
    }
    /**
     * Put ACLs to server and resolve promise when done.
     *
     * @param {Acl} acl
     * @return {$.jqXHR}
     */
    setAcl(acl) {
      const $deferred = new $.Deferred();
      const id = this.id;

      $.ajax({
        method: 'PUT',
        url: '/api/events/' + id + '/acl',
        dataType: 'json',
        data: {
          'acl': acl.getJSON(),
        },
      }).done(function() {
        $deferred.resolve();
      }).fail(function(r) {
        warn('PUT /api/events/' + id + '/acl failed.');
        $deferred.reject(r);
      });

      return $deferred.promise();
    }
    /**
     * Republish event's metadata if the event is already published
     * launching a WF instance
     *
     * @return {$.Promise}
     */
    republishMetadata() {
      const $deferred = new $.Deferred();
      const id = this.id;

      $.get('/api/events/' + id + '/publications').done(function(r) {
        let published = false;
        for (let i = 0; i < r.length; ++i) {
          const publication = r[i];
          if (publication.channel && publication.channel === 'engage-player') {
            published = true;
          }
        }
        if (!published) {
          $deferred.resolve('unpublished');
          return $deferred.promise();
        }
        $.post('/api/workflows/', {
          event_identifier: id,
          workflow_definition_identifier: REPUBLISH_METADATA_WF,
        }).done(function(r) {
          $deferred.resolve(r);
        }).fail(function(r) {
          warn('POST /api/workflows/ with event_identifier=' + id +
            ' and WDI=' + REPUBLISH_METADATA_WF + ' failed.');
          $deferred.reject(r);
        });
      }).fail(function(r) {
        warn('GET /api/events/' + id + '/publications failed.');
        $deferred.reject(r);
      });

      return $deferred.promise();
    }
  }

  /**
   * First, copy ACLs in Series, then in Episodes/Events
   * @param {RegExp} rolePattern
   * @param {string} roleReplace
   */
  function copyAcl(rolePattern, roleReplace) {
    Series.fromApi().done(function(series) {
      /**
       * Process the next series
       */
      function next() {
        if (!series.hasNext()) {
          copyAclEpisodes(rolePattern, roleReplace);
          return;
        }
        const serie = series.next();
        serie.getAcl().done(function(acl) {
          const changesMade = acl.duplicateRules(rolePattern, roleReplace);
          if (changesMade) {
            // Store changes if there are changes
            serie.setAcl(acl).done(function() {
              next();
            }).fail(function() {
              // Oh no! (setAcl)
              next();
            });
          } else {
            next();
          }
        }).fail(function() {
          // Oh no! (getAcl)
          next();
        });
      }
      next();
    }).fail(function() {
      // Oh no! (Series.fromApi)
      error('Fatal: Can\'t get Series.');
    });
  }

  /**
   * Copy ACLs in Episodes/Events
   * @param {RegExp} rolePattern
   * @param {string} roleReplace
   */
  function copyAclEpisodes(rolePattern, roleReplace) {
    Events.fromApi().done(function(events) {
      /**
       * Process the next event
       */
      function next() {
        if (!events.hasNext()) {
          log('done');
          return;
        }
        const event = events.next();
        event.getAcl().done(function(acl) {
          const changesMade = acl.duplicateRules(rolePattern, roleReplace);
          if (changesMade) {
            // Store changes if there are changes
            event.setAcl(acl).done(function() {
              event.republishMetadata().done(function() {
                setTimeout(next, REPUBLISH_SCHEDULE_DELAY);
              }).fail(function() {
                // Oh no! (republishMetadata)
                next();
              });
            }).fail(function() {
              // Oh no! (setAcl)
              next();
            });
          } else {
            next();
          }
        }).fail(function() {
          // Oh no! (getAcl)
          next();
        });
      }
      next();
    }).fail(function() {
      // Oh no! (Events.fromApi)
      error('Fatal: Can\'t get Events.');
    });
  }

  copyAcl(ROLE_PATTERN, ROLE_COPY);
}(window, jQuery));
