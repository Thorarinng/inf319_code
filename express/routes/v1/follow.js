const express = require("express");
const { ObjectId } = require("mongodb");
const router = express.Router();

// Models
const Follow = require("../../models/Follow");

router.get("/", async (req, res) => {
  const follow = await Follow.find();
  return res.json(follow);
});

router.post("/:userId", async (req, res) => {
  // User being followed
  const destinationId = req.params.userId;

  // User that pressed follow
  const sourceId = req.body.userId;

  if (destinationId === undefined)
    return res.send("Error: destinationId missing");
  if (sourceId === undefined) return res.send("Error: sourceId missing");

  const follow = await Follow.findOne({
    destination: destinationId,
    source: sourceId,
  });

  // Follow relationship does not exist
  if (follow === null) {
    // Create follow instance
    const follow = Follow({
      destination: destinationId,
      source: sourceId,
      isFollowing: true,
    });
    // Store to db
    await follow.save();
    return res.json(follow);
  }

  // Revert the current isFollowing boolean - store to db
  follow.isFollowing = !follow.isFollowing;
  await follow.save();
  return res.json(follow);
});

router.delete("/:username", async (req, res) => {});

module.exports = router;
