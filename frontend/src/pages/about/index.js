import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const About = ({ updateOrders, orders }) => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Заключительный проект от Яндекса Foodgram!</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Что такое Foodgram?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Foodgram - проект для проверки нашей работы на Django.
              Я не бекендер и вряд ли меня назовешь програмистом,
              я просто чиловый парень, обожающий вайб кодинг.
              Мечтаю уже закончить институт и не возращаться к It. 
              Я выгорел и у меня не осталось нервов, поэтому я уже ко всему отношусь со смехом,
              лучше пойду на завод на ямал нефть качать и попу морозить но лучше так чем так.
              К проекту не относитесь серьезно) прошу
            </p>
            <p className={styles.textItem}>
             Что было выполнено: 
            </p>
            <ul className={styles.featuresList}>
              <li>Создание и публикация собственных рецептов</li>
              <li>Добавление рецептов в избранное</li>
              <li>Формирование списка покупок для выбранных рецептов</li>
              <li>Подписка на других пользователей и их рецепты</li>
              <li>Удобный поиск рецептов по различным параметрам</li>
            </ul>
            <p className={styles.textItem}>
              Чтобы начать использовать все возможности Foodgram , просто зайтите на мой профиль гит, почитайте readme ну и там все понятно что как. если не понятно, то лучше не лезть, а то компьютер сломается
            </p>
          </div>
        </div>
        <aside>
          <h2 className={styles.additionalTitle}>
            Контакты
          </h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Исходный код проекта: <a href="https://github.com/bledbereq/foodgram-st" className={styles.textLink} target="_blank" rel="noopener noreferrer">GitHub</a>
            </p>
            <p className={styles.textItem}>
              Автор проекта: <a href="https://t.me/bledbereq" className={styles.textLink} target="_blank" rel="noopener noreferrer">TG: @bledbereq</a>
            </p>
          </div>
        </aside>
      </div>
    </Container>
  </Main>
}

export default About

