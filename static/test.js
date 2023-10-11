const fs = require("fs");

// read json file
const rawdata = fs.readFileSync("assets/json/export/scenario.json");

// convert json to object
const scenario = JSON.parse(rawdata);
// console.log(scenario);

//fetch id 3
const scenarioId = scenario.filter((item) => {
  return item.id === 3;
}).map;

// map nextId in id 3
const nextId = scenarioId.map((item) => {
  return item.nextId;
});

const nextIdObjects = scenario.filter((item) => {
  return nextId[0].includes(item.id);
});

console.log(nextIdObjects);
