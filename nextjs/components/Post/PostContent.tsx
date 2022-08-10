import React from "react";

import ps from "../../styles/Post.module.css";

export const PostContent = (props: { post: any }) => {
  const { post } = props;
  return (
    <div className={ps.comment}>
      {post.comment} <br />
    </div>
  );
};
