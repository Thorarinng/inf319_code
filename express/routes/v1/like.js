const express = require("express");
const { ObjectId } = require("mongodb");
const router = express.Router();

// Models
const Like = require("../../models/Like");
const Post = require("../../models/Post");

router.get("/", async (req, res) => {
  const likes = await Like.find();
  return res.json(likes);
});

router.get("/:postId", async (req, res) => {
  console.log("GET - /like/:postId");
  const { postId } = req.params;
  const likes = await Like.find({ post: postId });
  return res.json(likes);
});

router.post("/:postId", async (req, res) => {
  const { postId } = req.params;
  const { userId } = req.body;

  // Find post to like
  const post = await Post.findOne({ _id: ObjectId(postId) });

  // Post not found
  if (post === null)
    return res.send(
      `Error: Cannot like post. No post with id ${postId} found.`
    );

  // Does a like exist?
  const like = await Like.findOne({ post: postId, user: userId });

  console.log(like);

  if (like === null) {
    // Create like instance
    const like = Like({ post: postId, doesLike: true, user: userId });
    // Store to db
    await like.save();
    return res.json(like);
  }

  if (like.doesLike) {
    post.likeCount = post.likeCount - 1;
  } else {
    post.likeCount = post.likeCount + 1;
  }

  // Revert the current doesLike boolean - store to db
  like.doesLike = !like.doesLike;
  await like.save();
  await post.save();

  return res.json(like);
});

router.delete("/:username", async (req, res) => {});

module.exports = router;
