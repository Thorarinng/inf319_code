import type { NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import styles from "../../styles/Home.module.css";
import { Posts } from "../../components/Post/Posts";
import axios from "axios";
import Link from "next/link";

import { GetServerSideProps } from "next";
import { Followers } from "../../components/Follow/Followers";
import { Following } from "../../components/Follow/Following";

const Home: NextPage = (props: {
  posts: any;
  time: any;
  followers: any;
  following: any;
}) => {
  const { posts, followers, following, time } = props;
  return (
    <div className={styles.container}>
      <div className={styles.threeWay}>
        <div className={styles.twChild}>
          <p>A</p>
        </div>
        <div className={styles.twChild}>
          <p>B</p>
          <Posts posts={posts} />
          {time} milliseconds
          <br />
          <br />
          <br />
          <button>
            <Link href="/">Home</Link>
          </button>
        </div>
        <div className={styles.twChild}>
          <p>C</p>
          <Followers followers={followers} />
          <Following following={following} />
        </div>
      </div>
    </div>
  );
};

const getHomeScreenData = async () => {
  // HTTP REQUESTS
  // -> api/posts
  // -> api/user/id/:userId
  // -> api/like/:postId
  const query = `query {
    allFollowers {
      followers {
        id
        source {
          username
        }
      }
      following {
        id
        source {
          username
        }
        destination {
          username
        }
      }
    }
    allPosts{
      posts{
        id,
        comment,
        likeCount,
        parent{
          id
        },
        user {
          id,
          username,firstname,lastname,imgURL,date
          
        }
      }
    }
  }`;
  const startTime = performance.now();
  const res = await axios.post("graphql/", {
    query: query,
  });
  const endTime = performance.now();
  //   console.log(res.data);
  const { allFollowers, allPosts } = res.data.data;
  const { followers, following } = allFollowers;
  const { posts } = allPosts;

  console.log(followers);
  console.log(following);
  console.log(posts);

  return { posts, followers, following, time: endTime - startTime };
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  const token =
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxNDIzMTIwLCJpYXQiOjE2NDk0MjMxMjAsImp0aSI6IjBjNTY3NzI1NjY3YzQwMmY5NjAzZGNkNTYwNjRkNzcwIiwidXNlcl9pZCI6MX0.uzGnzzLWsBs2ZS9IId2RmJg6jw7gYO1tUqP2LUuV5LM";

  axios.defaults.baseURL = "http://localhost:8000/";
  axios.defaults.headers.common = { Authorization: `bearer ${token}` };

  const { posts, followers, following, time } = await getHomeScreenData();
  await getHomeScreenData();

  return {
    props: {
      posts,
      followers,
      following,
      time,
    },
  };
};

export default Home;
