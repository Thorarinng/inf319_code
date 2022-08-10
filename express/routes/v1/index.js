const express = require("express");
const router = express.Router();

const user = require("./user.js");
const post = require("./post.js");
const like = require("./like.js");
const follow = require("./follow.js");

// Add endpoint object types here
router.use("/user", user);
router.use("/post", post);
router.use("/like", like);
router.use("/follow", follow);

module.exports = router;
