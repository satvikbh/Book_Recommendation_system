import express from "express";
import bodyParser from "body-parser";
import session from "express-session";
import { dirname } from "path";
import { fileURLToPath } from "url";
const __dirname = dirname(fileURLToPath(import.meta.url));

const app = express();
const port = 3000;


app.use(session({
  secret: 'muskan', 
  resave: false,
  saveUninitialized: true
}));
app.use(express.static("views"));
app.use(bodyParser.urlencoded({ extended: true }));

// Middleware to check password
function passwordCheck(req, res, next) {
  const password = req.body["password"];
  if (password === "muskan") {
    req.session.userIsAuthorised = true;
  }
  next();
}

// Apply the middleware only to the POST /check route
app.post("/check", passwordCheck, (req, res) => {
  if (req.session.userIsAuthorised) {
    res.sendFile(__dirname + "/public/carousel.html");
  } else {
    res.sendFile(__dirname + "/public/carousel.html");
  }
});

// Route for the root
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/public/index.html");
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
