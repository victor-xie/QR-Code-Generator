# QR-Code-Generator
This project seeks to develop a method of creating more easily scannable QR codes through error correction.


### What's So Special About QR Codes?
Ever wonder why QR codes still work even though you don't scan them perfectly aligned or if some parts of the code is covered? This is because QR codes have error correction built into them. This design allows users to scan QR codes more easily, without having to worry about including all portions of the code in perfect view of the camera.

### What's the Goal of This Project?
This project seeks to maximize the reliability of QR codes through Reed-Solomon error correction. In experimental trials, this approach to embedding error correction within QR codes resulted in a less than 1% failure-to-scan rate in the 1000 user trials run during experimental testing.

### What is Reed-Solomon Error Correction?
Reed-Solomon is a type of error correction that functions within a finite field (in a similar branch of mathematics as modulus). By dividing polynomials representing a message by a "generator polynomial," a polynomial representing the error correction bits is produced. 

### How Was Reed-Solomon Implemented in This Project?
First, I built a Polynomial class with relevant methods that, importantly, did not mutate an object's fields and instead returned new objects. This is an intentional design choice to prevent unwanted data mutation. Class methods include typical behaviors one would expect of polynomials, such as multiplication, addition, and subtraction.

The rest of the functions calculate the message, generator, and remainder polynomials. The remainder polynomial is the final desired product, as it will become the error correction bits embedded into the QR code.

### Project Demo
This GUI allows the user to input a string of text and generates a QR code that searches that text on the web. If a URL is inputted, as is shown in the last part of the demo, the user is taken to that website. Feel free to try it out!

https://user-images.githubusercontent.com/84203383/146310604-735dee17-8c92-4c24-a14e-f1bb6e00cbf7.mov


