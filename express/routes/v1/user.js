const express = require("express");
const router = express.Router();

// Models
const User = require("../../models/User");

router.get("/", async (req, res) => {
  const users = await User.find();
  res.json(users);
});

router.post("/", async (req, res) => {
  const { username, firstname, lastname, imgURL, password } = req.body;

  try {
    const user = new User({ username, firstname, lastname, imgURL, password });
    console.log(user);
    await user.save();
    res.status(201).send(user);
  } catch (e) {
    console.log(e._message);
    res.status(400).send(e._message);
  }
});

router.get("/:username", async (req, res) => {
  const { username } = req.params;
  const user = await User.findOne({ username });
  res.send(user);
});

router.delete("/:username", async (req, res) => {
  const { username } = req.params;
  const user = await User.findOneAndDelete({ username });

  if (user === null)
    return res.send(`User with username: ${username} was not found`);

  res.json(user);
});

router.get("/id/:userId", async (req, res) => {
  console.log("GET - /user/id/:userId");
  const { userId } = req.params;
  const users = await User.findOne({ _id: userId });
  res.json(users);
});

module.exports = router;
