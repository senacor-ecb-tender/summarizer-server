<template>
  <div class="q-pa-md bg-image">
    <q-page class="flex flex-top ecb-font-bold">
      <div class="fit row-xs wrap justify-start items-start content-start ">
        <div class="col-grow">
          <div align="center" class="text-h3 text-primary">Let us make your content understandable</div>
          <br>
          <div align="center"><q-img align="center" width="33%" src="~assets/logo_partnership.jpg"/></div>

        </div>
      </div>
      <div class="fit row wrap justify-center items-start content-start q-gutter-x-md">
        <div class="col-3">
          <q-card style="height: 200px">
            <q-card-section>
              <q-avatar rounded color="secondary" text-color="secondary"></q-avatar>
              <br>
              <div class="text-h4" align="center">Setting up</div>
              <br>
              <div class="ecb-font-regular text-body1" align="center">Select the topic, summary length and your text file you want to summarize</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-3">
          <q-card style="height: 200px">
            <q-card-section>
              <q-avatar rounded color="secondary" text-color="secondary">2</q-avatar>
              <div class="text-h4" align="center">Summarizing</div>
              <br>
              <div class="ecb-font-regular text-body1" align="center">Run our
                state-of-the-art summarization based on newest NLP algorithms
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-3">
          <q-card style="height: 200px">
            <q-card-section>
              <q-avatar rounded color="secondary" text-color="secondary">3</q-avatar>
              <br>
              <div class="text-h4" align="center">Enjoying</div>
              <br>
              <div class="ecb-font-regular text-body1" align="center">Enjoy the new insights due to complexity reduction
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-page>
  </div>
</template>
<style>
.bg-image {
  background-image: url("../assets/background-landing.png");
  background-repeat: no-repeat;
  background-size: 100% 80%;
  background-position: bottom;
}
</style>
<script>
export default {
  name: 'PageIndex'
}
</script>
