import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'
import toolsImg from '../../images/tools-img.jpg'

const Technologies = () => {
  
  return <Main>
    <MetaTags>
      <title>Технологии проекта</title>
      <meta name="description" content="Фудграм - Технологии проекта" />
      <meta property="og:title" content="Технологии проекта" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Технологии проекта</h1>
      <div className={styles.content}>
        <div className={styles.mainSection}>
          <div className={styles.imageContainer}>
            <img src={toolsImg} alt="Инструменты разработки" className={styles.image} />
          </div>
          <div className={styles.techSection}>
            <h2 className={styles.subtitle}>Технологии</h2>
            <div className={styles.text}>
              <ul className={styles.techList}>
                <li className={styles.techItem}>Django REST Framework - для создания API</li>
                <li className={styles.techItem}>Djoser - для аутентификации</li>
                <li className={styles.techItem}>PostgreSQL - база данных</li>
                <li className={styles.techItem}>Docker - контейнеризация</li>
                <li className={styles.techItem}>Nginx - веб-сервер</li>
                <li className={styles.techItem}>GitHub Actions - CI/CD</li>
                <li className={styles.techItem}>Pillow - работа с изображениями</li>
                <li className={styles.techItem}>Pytest - тестирование</li>
                <li className={styles.techItem}>Gunicorn - WSGI-сервер</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </Container>
  </Main>
}

export default Technologies

