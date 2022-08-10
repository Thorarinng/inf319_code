import React, { useState } from "react";

const CreatePost = () => {
  const [text, setText] = useState("");

  const handleSubmit = async () => {};

  return (
    <>
      <br />
      <input
        placeholder="Comment"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button type="button" onClick={handleSubmit}>
        Post
      </button>
    </>
  );
};

export default CreatePost;
