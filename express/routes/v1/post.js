const express = require("express");
const { ObjectId } = require("mongodb");
const router = express.Router();

// Models
const Post = require("../../models/Post");

router.get("/", async (req, res) => {
  const posts = await Post.find();
  return res.json(posts);
});

router.post("/", async (req, res) => {
  const { comment, parent, userId } = req.body;

  if (userId === undefined) return res.send("Error: User ObjectId missing");

  const post = Post({ comment, parent, user: userId });

  await post.save();

  return res.json(post);
});

router.get("/:postId", async (req, res) => {
  const { postId } = req.params;
  console.log(postId);
  console.log(ObjectId(postId));
  const post = await Post.findOne({ _id: ObjectId(postId) });

  if (post === null) return res.send(`Error: No post with id ${postId} found.`);

  return res.json(post);
});

router.delete("/:username", async (req, res) => {});

module.exports = router;
