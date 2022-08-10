import type { NextPage } from "next";
import Link from "next/link";
import styles from "../styles/Home.module.css";

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <div className={styles.threeWay}>
        <div className={styles.twChild}>
          <p>Naive Model</p>
          <button>
            <Link href="/naivemodel"> Naive Model</Link>
          </button>
        </div>
        <div className={styles.twChild}>
          <p>REST Model</p>
          <button>
            <Link href="/restmodel"> REST Model</Link>
          </button>
        </div>
        <div className={styles.twChild}>
          <p>GraphQL Model</p>
          <button>
            <Link href="/graphqlmodel"> GraphQL Model</Link>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
