// Problematic JavaScript code for testing code review tools
// This file intentionally contains various syntax errors and anti-patterns

import {something,another,third} from 'module'; // Bad: no spaces after commas

// Magic numbers and poor function naming
function CalculateScore(data){ // Bad: no space before brace, CamelCase
var total=0; // Bad: var instead of let/const, no spaces
for(var i=0;i<data.length;i++){ // Bad: no spaces, var instead of let
if(data[i]>100){ // Bad: no spaces, magic number
total+=data[i]*2; // Bad: magic number
}else if(data[i]>50&&data[i]<=100){ // Bad: no spaces, magic numbers
total+=data[i]*1.5;
}else if(data[i]>25){
total+=data[i];
}else if(data[i]>10){
total+=data[i]*0.5;
}else{
total+=0;
}
}
return total;
}

// Class with too many responsibilities (God object)
class DataManager{ // Manager pattern + anti-pattern
constructor(){
this.data=[];
this.cache={};
this.settings={};
this.users=[];
this.logs=[];
this.stats={};
this.tempData=[];
this.processedItems=[];
this.failedItems=[];
this.successCount=0;
this.errorCount=0;
this.lastUpdated=null;
this.isDirty=false; // Too many properties
}

processData(input,mode,options,filters,validators,transformers,handlers,callbacks){ // Too many parameters
if(!input)return[]; // Bad: no space after if

let result=[];
let errors=[];

for(let i=0;i<input.length;i++){
let item=input[i];

if(mode==='strict'){
if(options&&options.validate){
if(validators){
for(let j=0;j<validators.length;j++){
let validator=validators[j];
if(validator==='email'){
if(typeof item!=='string'||item.indexOf('@')===-1||item.indexOf('.')===-1){
errors.push(`Invalid email at index ${i}`);
continue;
}
}else if(validator==='phone'){
if(typeof item!=='string'||item.length!==10){ // Magic number
errors.push(`Invalid phone at index ${i}`);
continue;
}
}else if(validator==='age'){
let age=parseInt(item);
if(age<18||age>120){ // Magic numbers
errors.push(`Invalid age at index ${i}`);
continue;
}
}
}
}
}

if(transformers){
for(let k=0;k<transformers.length;k++){
let transformer=transformers[k];
if(transformer==='uppercase'){
item=item.toString().toUpperCase();
}else if(transformer==='lowercase'){
item=item.toString().toLowerCase();
}else if(transformer==='trim'){
item=item.toString().trim();
}
}
}

result.push(item);
}else if(mode==='lenient'){
try{
result.push(item);
}catch(e){
errors.push(`Error processing item at index ${i}`);
}
}
}

return{result:result,errors:errors}; // Should return [result, errors] for consistency
} // Very long function with high complexity
}

function createUserFactory(type){ // Factory pattern
if(type==='admin'){
return{type:'admin',permissions:['read','write','delete']};
}else if(type==='user'){
return{type:'user',permissions:['read']};
}else{
return{type:'guest',permissions:[]};
}
}

class ConfigBuilder{ // Builder pattern
constructor(){
this.config={};
}

buildDatabaseConfig(){
this.config.database={host:'localhost',port:5432}; // Magic number
return this;
}

buildCacheConfig(){
this.config.cache={ttl:3600,maxSize:1000}; // Magic numbers
return this;
}

build(){
return this.config;
}
}

// Singleton pattern
class Logger{
constructor(){
if(Logger.instance){
return Logger.instance;
}
Logger.instance=this;
}

static getInstance(){
if(!Logger.instance){
Logger.instance=new Logger();
}
return Logger.instance;
}
}

// Syntax errors
function brokenFunction() {
let x = 10
let y = 20; // Missing semicolon above
if(x > y {  // Missing closing parenthesis
return x + y;
}

// Very long line that exceeds reasonable limits and should be flagged by any decent style checker as a violation that needs to be addressed immediately
let longVariable = "This is an extremely long string that definitely exceeds any reasonable line length limit and should be broken up into multiple lines for better readability and maintainability";

function processEverything(data,mode,settings,cache,logs,users,permissions,filters,validators,transformers,handlers,callbacks,options,config){ // Too many parameters
// Empty function
}

// Main execution with problems
if(__name__==="main"){ // Bad: should be different check for JS
let data=[1,2,3,42,100,1000]; // Magic numbers, no spaces
let score=CalculateScore(data);
console.log("Score: "+score); // Should use template literals

let manager=new DataManager();
let result=manager.processData(data,'strict',null,null,null,null,null,null);
console.log("Processed: "+result.result.length+" items");
}